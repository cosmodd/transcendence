import { Injectable } from '@nestjs/common';
import { User } from './user/user.entity';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';

@Injectable()
export class AppService {
	constructor(
		@InjectRepository(User)
		private readonly userRepository: Repository<User>,
	) {
		const placeholderUser: User = {
			id: 1,
			name: "Eric Zemmour",
			age: 30,
			race: "Caucasian",
		};
		this.Create(placeholderUser);
	}

	async Create(userData: User): Promise<User> {
		const newUser = this.userRepository.create(userData);
		return await this.userRepository.save(newUser);
	}

  	async FindAll(): Promise<User[]> {
    	return await this.userRepository.find();
  	}
}
