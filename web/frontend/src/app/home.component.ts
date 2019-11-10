import { Component, OnInit } from '@angular/core';
import { BotService } from './services/bot.service';

@Component({
  selector: 'app-home',
  template: `
  <div>
    <button class="button">Add to Discord</button>
  </div>
  `,
  styles: []
})
export class HomeComponent implements OnInit {

  constructor(private botService: BotService) { }

  ngOnInit() {
  }

}
