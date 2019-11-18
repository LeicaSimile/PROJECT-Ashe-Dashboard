import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class BotService {
  botName = 'PROJECT Ashe';
  constructor() { }

  getStatus() {
    return;
  }

  getNumberServers(): number {
    return 1;
  }
}
