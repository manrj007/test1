import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { MainContainerComponent } from './main-container/main-container.component';
import { CompareComponent } from './compare/compare.component';
import { ViewComponent } from './view/view.component';
import { OutputComponent } from './output/output.component';

const routes: Routes = [
  { path: '', redirectTo: '/main', pathMatch: 'full' },
  { path: 'main', component: MainContainerComponent },
  { path: 'compare', component: CompareComponent },
  { path: 'view', component: ViewComponent },
  { path: 'output', component: OutputComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
