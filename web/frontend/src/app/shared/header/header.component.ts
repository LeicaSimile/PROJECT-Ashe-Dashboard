import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-header',
  template: `
    <nav class="navbar is-fixed-top level" role="navigation" aria-label="main navigation">
      <div class="navbar-brand level-left">
        <div class="level-item">
          <a routerLink=""><h1 class="is-uppercase has-text-light">PROJECT Ashe</h1></a>
        </div>
      </div>
      <div class="level-right">
        <div class="level-item">
          <button class="button is-primary is-outlined">Login</button>
        </div>
      </div>
    </nav>
  `, styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }

}
