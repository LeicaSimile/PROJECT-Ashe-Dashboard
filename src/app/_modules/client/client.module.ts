import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ClientRoutingModule } from './client-routing.module';
import { SharedModule } from '../shared/shared.module';
import { ClientComponent } from './client.component';
import { DashboardComponent } from './dashboard/dashboard.component';


@NgModule({
  declarations: [ClientComponent, DashboardComponent],
  imports: [
    CommonModule,
    ClientRoutingModule,
    SharedModule
  ],
  exports: [
    ClientComponent
  ]
})
export class ClientModule { }
