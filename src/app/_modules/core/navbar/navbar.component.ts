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
    const destination = 'https://discord.com/api/oauth2/authorize';
    const redirect = encodeURIComponent('http://localhost:4200/auth');
    const scope = encodeURIComponent('identify guilds');

    this.router.navigate([`/${this.app.externalUrl}`, {
      externalUrl: `${destination}?client_id=${this.app.CLIENT_ID}&redirect_uri=${redirect}&response_type=code&scope=${scope}`
    }], {
      skipLocationChange: true
    });
  }
}
