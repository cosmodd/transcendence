import { Controller, Get, Post, Body } from '@nestjs/common';
import { AppService } from './app.service';
import { createUserDto } from './dto/user.dto';
import { User } from './interfaces/user.interface';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get()
  async FindAll(): Promise<User[]> {
    return this.appService.FindAll();
  }

  @Post()
  async Create(@Body() createUserDto: createUserDto) {
	  this.appService.Create(createUserDto);
  }
}
