import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { TypeOrmModule } from '@nestjs/typeorm';
import { User } from './user/user.entity';

const path = require("path");

@Module({
	imports: [TypeOrmModule.forRoot({
		"type": "postgres",
		"host": "postgres",
		"port": 5432,
		"username": "user",
		"password": "password",
		"database": "transcendence-db",
		"synchronize": true,
		"logging": true,
		"entities": [path.join(__dirname, '**', '*.entity.{ts,js}')]
	}),
	TypeOrmModule.forFeature([User])],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
