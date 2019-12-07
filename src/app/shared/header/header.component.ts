import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-header',
  template: `
    <nav class="navbar is-fixed-top level" role="navigation" aria-label="main navigation">
      <div class="level-left">
        <div class="navbar-brand level-item">
          <a routerLink=""><h1 class="is-uppercase has-text-light">PROJECT Ashe</h1></a>
        </div>
        <a routerLink="" class="level-item">Home</a>
        <a routerLink="" class="level-item">Features</a>
        <a routerLink="" class="level-item">Documentation</a>
        <a routerLink="" class="level-item">Contact</a>
      </div>
      <div class="level-right">
        <div class="level-item">
          <form>
            <button class="button is-primary is-outlined" formaction="http://localhost:3000/api/login">Login</button>
          </form>
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
