import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { CoreComponent } from './_modules/core/core.component';


const routes: Routes = [
  {
    path: '',
    component: CoreComponent,
    pathMatch: 'full'
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
