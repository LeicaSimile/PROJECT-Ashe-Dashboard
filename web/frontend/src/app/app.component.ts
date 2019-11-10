import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  template: `
  <div class="header">
    <app-header></app-header>
  </div>
  <main class="container">
    <router-outlet></router-outlet>
  </main>
  `
})
export class AppComponent {}
