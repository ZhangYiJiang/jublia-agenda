import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule } from '@angular/router';
import { HttpModule, JsonpModule } from '@angular/http';
import { DragulaService, DragulaModule } from 'ng2-dragula/ng2-dragula';
import { MaterialModule } from '@angular/material';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { TagInputModule } from 'ng2-tag-input';

import { AppComponent } from './app.component';

import { BoardComponent } from './board/board.component.ts';
import { AbsoluteColumnComponent } from './absolute-column/absolute-column.component.ts';
import { RelativeColumnComponent } from './relative-column/relative-column.component.ts';
import { SessionComponent } from './session/session.component.ts';
import { DashBoardComponent } from './dash-board/dash-board.component.ts';
import { AgendaComponent } from './agenda/agenda.component.ts';
import { PublicAgendaComponent } from './public-agenda/public-agenda.component.ts';
import { AnalyticsComponent } from './analytics/analytics.component.ts';
import { AgendaService } from './agenda/agenda.service.ts';
import { DashBoardService } from './dash-board/dash-board.service.ts';
import { BoardService } from './board/board.service.ts';
import { PublicAgendaService } from './public-agenda/public-agenda.service.ts';
import { LineChartComponent } from './chart/chart.component.ts';

import { DOMUtilService } from './util/dom.util.service';
import { HttpClient } from './util/http.util.service';
import { User } from './util/user.util.service';

import { OrderBy } from './pipes/orderby.pipe';
import { Where } from './pipes/where.pipe';
import { EncodeURIComponentPipe } from 'angular-pipes/src/string/encode-uri-component.pipe';
import { EncodeURIPipe } from 'angular-pipes/src/string/encode-uri.pipe';

import { LoggedInGuard } from './auth.guard.ts';

import { ModalModule } from 'angular2-modal';
import { VexModalModule} from 'angular2-modal/plugins/vex';
import { JwtHelper } from 'angular2-jwt';


import { NdvEditComponent } from './ndv/ndv.edit.component.ts';
import { NdvEditAreaComponent } from './ndv/ndv.edit.area.component.ts';

import { ChartsModule } from 'ng2-charts/ng2-charts';
import { ClipboardModule } from 'angular2-clipboard';

@NgModule({
  imports: [
    BrowserModule,
    HttpModule,
    JsonpModule,
    RouterModule.forRoot([
      //order matters, goes to first match
      { path: 'agenda/:id', component: AgendaComponent, canActivate: [LoggedInGuard] },
      { path: 'public/agenda/:id/:token', component: PublicAgendaComponent },
      { path: 'public/agenda/:id', component: PublicAgendaComponent },
      { path: 'analytics/agenda/:id', component: AnalyticsComponent, canActivate: [LoggedInGuard] },
      { path: '', component: DashBoardComponent },
      { path: '**', component: DashBoardComponent } // TODO: implement 404 page component
    ]),
    DragulaModule,
    MaterialModule.forRoot(),
    FormsModule,
    ReactiveFormsModule,
    TagInputModule,
    ModalModule.forRoot(),
    VexModalModule,
    ChartsModule,
    ClipboardModule,
  ],
  declarations: [
    AppComponent,
    BoardComponent,
    AbsoluteColumnComponent,
    RelativeColumnComponent,
    SessionComponent,
    DashBoardComponent,
    AgendaComponent,
    PublicAgendaComponent,
    AnalyticsComponent,
    
    OrderBy,
    Where,
    EncodeURIComponentPipe,
    EncodeURIPipe,
    
    NdvEditComponent,
    NdvEditAreaComponent,
    LineChartComponent
  ],
  providers: [
    AgendaService,
    DashBoardService,
    BoardService,
    PublicAgendaService,
    LoggedInGuard,
    DOMUtilService,
    HttpClient,
    JwtHelper,
    User
  ],
  bootstrap: [ AppComponent ]
})
export class AppModule { }