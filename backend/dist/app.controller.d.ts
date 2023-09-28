import { AppService } from './app.service';
import { createUserDto } from './dto/user.dto';
import { User } from './interfaces/user.interface';
export declare class AppController {
    private readonly appService;
    constructor(appService: AppService);
    FindAll(): Promise<User[]>;
    Create(createUserDto: createUserDto): Promise<void>;
}
