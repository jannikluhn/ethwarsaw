import { Controller, Get, Param, Post, Res } from '@nestjs/common';
import { BigNumberish, ethers } from 'ethers';
import { Response, response } from 'express';
import { RedisService } from 'src/redis/redis.service';

type EncounterGameResponse = {
  status: string;
  answer: string;
  correctAnswer?: string;
  tokenId?: BigNumberish;
  eligibleMinter?: string;
  uriIndex?: string;
  chainId?: string;
  authorizationSignature?: string;
};

@Controller('encounters')
export class EncountersController {
  constructor(private readonly redisService: RedisService) {}

  async createResponseBody(
    game: string[],
    encounter: string[],
  ): Promise<EncounterGameResponse> {
    const [status, answer, correctAnswer] = game;
    const [tokenId, chainId, user] = encounter;
    console.log(tokenId, chainId);
    const responseBody: EncounterGameResponse = {
      status,
      answer,
    };

    if (answer) {
      responseBody.correctAnswer = correctAnswer;
    }

    if (status === 'success') {
      const signer = new ethers.Wallet(process.env.PRIVATE_KEY || '');
      responseBody.uriIndex = '1';
      responseBody.tokenId = tokenId;
      responseBody.chainId = chainId;
      responseBody.eligibleMinter = user.split(':')[1];
      const mintMessage = ethers.solidityPacked(
        ['address', 'uint256', 'uint256'],
        [responseBody.eligibleMinter, responseBody.tokenId, 1],
      );
      responseBody.authorizationSignature = await signer.signMessage(
        ethers.getBytes(mintMessage),
      );
    }

    return responseBody;
  }

  @Get('/game/:encounterId')
  async getEncounterGame(
    @Res() res: Response,
    @Param('encounterId') encounterId: string,
  ) {
    const exists = await this.redisService.encounterGameExists(encounterId);

    if (!exists) {
      return res.status(404).json({
        message: 'Game not found.',
        data: undefined,
      });
    }

    const game = await this.redisService.getEncounterGame(encounterId);
    const encounter = await this.redisService.getEncounter(encounterId);

    if (game.length) {
      return res.json({
        message: undefined,
        data: await this.createResponseBody(game, encounter),
      });
    }
  }

  @Post('/game/:encounterId/:answerIndex')
  async submitGameResult(
    @Res() res: Response,
    @Param('encounterId') encounterId: string,
    @Param('answerIndex') answerIndex: string,
  ) {
    try {
      let game = await this.redisService.getEncounterGame(encounterId);

      const [_, answer] = game;
      if (answer) {
        throw new Error('Re-submissions are not allowed.');
      }

      if (game) {
        await this.redisService.submitEncounterGameAnswer(
          encounterId,
          answerIndex,
        );
        await this.redisService.publishNewGameAnswer(encounterId);
      }

      game = await this.redisService.getEncounterGame(encounterId);
      const encounter = await this.redisService.getEncounter(encounterId);

      return res.json({
        message: 'Successfully submitted answer.',
        data: await this.createResponseBody(game, encounter),
      });
    } catch (e) {
      return res.status(500).json({
        message: e.message,
      });
    }
  }
}
