import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-header',
  template: `
    <nav class="navbar is-fixed-top level has-background-primary" role="navigation" aria-label="main navigation">
      <div class="navbar-brand level-left">
        <div class="level-item">
          <a routerLink=""><h1 class="is-uppercase has-text-light">PROJECT Ashe</h1></a>
        </div>
      </div>
    </nav>
  `
})
export class HeaderComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }

}
