import { NgModule, InjectionToken } from '@angular/core';
import { Routes, RouterModule, ActivatedRouteSnapshot } from '@angular/router';
import { CoreComponent } from './_modules/core/core.component';
import { ClientComponent } from './_modules/client/client.component';
import { AuthComponent } from './_modules/core/auth/auth.component';

const externalUrlProvider = new InjectionToken('externalUrlRedirectResolver');
const routes: Routes = [
  {
    path: '',
    component: CoreComponent,
    pathMatch: 'full'
  },
  {
    path: 'user',
    component: ClientComponent
  },
  {
    path: 'externalRedirect',
    resolve: {
      url: externalUrlProvider
    },
    component: CoreComponent
  },
  {
    path: 'auth',
    component: AuthComponent
  },
  {
    path: '**',
    component: CoreComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
  providers: [
    {
        provide: externalUrlProvider,
        useValue: (route: ActivatedRouteSnapshot) => {
            const externalUrl = route.paramMap.get('externalUrl');
            window.open(externalUrl, '_self');
        },
    },
],
})
export class AppRoutingModule { }
