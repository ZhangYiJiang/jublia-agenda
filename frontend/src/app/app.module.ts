import { NgModule } from '@angular/core';
import { BrowserModule }  from '@angular/platform-browser';
import { AppComponent } from './app.component';

import { BoardComponent } from './board/board.component.ts';

@NgModule({
  imports: [
    BrowserModule
  ],
  declarations: [
    AppComponent,
    BoardComponent
  ],
  bootstrap: [ AppComponent ]
})
export class AppModule { }