import { User } from './interfaces/user.interface';
export declare class AppService {
    private readonly users;
    constructor();
    Create(user: User): void;
    FindAll(): User[];
}
