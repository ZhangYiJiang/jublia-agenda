import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule } from '@angular/router';
import { HttpModule, JsonpModule } from '@angular/http';
import { DragulaService, DragulaModule } from 'ng2-dragula/ng2-dragula';

import { AppComponent } from './app.component';

import { BoardComponent } from './board/board.component.ts';
import { AbsoluteColumnComponent } from './absolute-column/absolute-column.component.ts';
import { RelativeColumnComponent } from './relative-column/relative-column.component.ts';
import { SessionComponent } from './session/session.component.ts';
import { DashBoardComponent } from './dash-board/dash-board.component.ts';

import { AgendaComponent } from './agenda/agenda.component.ts';
import { AgendaService } from './agenda/agenda.service.ts';

import {OrderBy} from './pipes/orderby.pipe';
import {Where} from './pipes/where.pipe';


@NgModule({
  imports: [
    BrowserModule,
    HttpModule,
    JsonpModule,
    RouterModule.forRoot([
      { path: 'agenda/:id', component: AgendaComponent },
      { path: '', component: DashBoardComponent },
      { path: '**', component: DashBoardComponent }
    ]),
    DragulaModule
  ],
  declarations: [
    AppComponent,
    BoardComponent,
    AbsoluteColumnComponent,
    RelativeColumnComponent,
    SessionComponent,
    DashBoardComponent,
    AgendaComponent,
    OrderBy,
    Where
  ],
  providers: [
    AgendaService
  ],
  bootstrap: [ AppComponent ]
})
export class AppModule { }