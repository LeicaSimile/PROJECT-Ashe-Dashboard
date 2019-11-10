import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-header',
  template: `
    <nav class="navbar is-fixed-top" role="navigation" aria-label="main navigation">
      <div class="navbar-header">
        <a routerLink=""><h1 class="navbar-brand">PROJECT Ashe</h1></a>
      </div>
    </nav>
  `
})
export class HeaderComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }

}
