import { Injectable } from '@nestjs/common';
import { User } from './interfaces/user.interface';

@Injectable()
export class AppService {
	private readonly users: User[] = [];

	constructor() {
		const placeholderUser: User = {
			age: 30,
			name: "Eric Zemmour",
			race: "Caucasian",
		};
		this.users.push(placeholderUser);
	}

	Create(user: User) {
		this.users.push(user);
	}

  	FindAll(): User[] {
    	return this.users;
  	}
}
