import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { CoreComponent } from './_modules/core/core.component';
import { ClientComponent } from './_modules/client/client.component';


const routes: Routes = [
  {
    path: '',
    component: CoreComponent,
    pathMatch: 'full'
  }, {
    path: 'user',
    component: ClientComponent
  }, {
    path: '**',
    component: CoreComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
