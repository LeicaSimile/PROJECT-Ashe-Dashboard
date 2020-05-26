import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AppService } from '../../shared/_services/app.service';

@Component({
  selector: 'app-auth',
  templateUrl: './auth.component.html'
})
export class AuthComponent implements OnInit {

  constructor(private route: ActivatedRoute, private router: Router, private app: AppService) {}

  ngOnInit() {
    const code = this.route.snapshot.queryParamMap.get('code');
    const error = this.route.snapshot.queryParamMap.get('error');
    if (error) {
      this.router.navigateByUrl('/');
      return;
    }

    if (this.app.user) {
      this.router.navigateByUrl('/user/dashboard');
    } else {
      console.log(this.route.snapshot.queryParams);
      this.router.navigateByUrl('/');
    }
  }

}
