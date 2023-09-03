import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { SiweController } from './siwe/siwe.controller';
import { RedisModule } from './redis/redis.module';
import { EncountersController } from './encounters/encounters.controller';
import { ConfigModule } from '@nestjs/config';
@Module({
  imports: [ConfigModule.forRoot(), RedisModule],
  controllers: [AppController, SiweController, EncountersController],
  providers: [AppService],
})
export class AppModule {}
