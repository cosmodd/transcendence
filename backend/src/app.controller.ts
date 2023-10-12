import { Controller, Get, Post, Body } from '@nestjs/common';
import { AppService } from './app.service';
import { User } from './user/user.entity';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get()
  async FindAll(): Promise<User[]> {
    return this.appService.FindAll();
  }

  @Post()
  async Create(@Body() user: User) {
	  this.appService.Create(user);
  }
}
