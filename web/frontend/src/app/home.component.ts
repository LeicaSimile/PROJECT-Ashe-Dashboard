import { Component, OnInit } from '@angular/core';
import { BotService } from './services/bot.service';

@Component({
  selector: 'app-home',
  template: `
  <div>
    <h1 class="title">Discord moderation for humanity.</h1>
    <h3 class="subtitle has-text-grey-light">Includes x, y, z, and more.</h3>
    <button class="button is-primary is-large">Add to Discord</button>
  </div>
  `,
  styles: []
})
export class HomeComponent implements OnInit {

  constructor(private botService: BotService) { }

  ngOnInit() {
  }

}
