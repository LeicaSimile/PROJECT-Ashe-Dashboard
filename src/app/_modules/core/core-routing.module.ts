import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { CoreComponent } from './core.component';
import { HomeComponent } from './home/home.component';
import { AuthComponent } from './auth/auth.component';
const coreRoutes: Routes = [
    {
        path: '',
        component: CoreComponent,
        children: [
            {
                path: '',
                component: HomeComponent,
                pathMatch: 'full'
            },
            {
                path: 'auth',
                component: AuthComponent
            }
        ]
    }
];
@NgModule({
    imports: [RouterModule.forChild(coreRoutes)],
    exports: [RouterModule]
})
export class CoreRoutingModule { }
