import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AppService } from '../../shared/_services/app.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html'
})
export class NavbarComponent implements OnInit {
  constructor(private router: Router, private app: AppService) { }

  ngOnInit() {
  }

  login() {
    this.router.navigate([`/${this.app.externalUrl}`, {
      externalUrl: 'https://discord.com/api/oauth2/authorize?client_id=323173717968683019&redirect_uri=http%3A%2F%2Flocalhost%3A4200%2Fuser%2Fdashboard&response_type=code&scope=identify%20guilds'
    }], {
      skipLocationChange: true
    });
  }
}
