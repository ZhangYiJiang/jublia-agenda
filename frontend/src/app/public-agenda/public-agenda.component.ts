import { Input, Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';

import { Session } from '../session/session';
import { Agenda } from '../agenda/agenda';
import { AgendaService } from '../agenda/agenda.service';
import { DashBoardService } from '../dash-board/dash-board.service';
import { PublicAgendaService } from './public-agenda.service';

@Component({
  selector: 'public-agenda',
  templateUrl: './public-agenda.component.html',
  styleUrls: ['./public-agenda.component.css']
})
export class PublicAgendaComponent implements OnInit{
  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private agendaService: AgendaService,
    private dashBoardService: DashBoardService,
    private publicAgendaService: PublicAgendaService) { }
  
  user = this.dashBoardService.currentUser;
  agenda: Agenda;
  email: string;
  agendaId: number;
  token : string;
  interestedSessionIds: number[];
  
  ngOnInit() {
    this.route.params.forEach((params: Params) => {
      this.agendaId = params['id'];
      this.getAgendaById(this.agendaId);

      this.token = params['token'];
      if (this.token) {
        this.getViewerByToken(this.token);
      }
    });
  }

  getAgendaById(id: number) {
    this.agendaService.getAgendaById(id).subscribe(
        agenda => {if (agenda.published) {this.agenda = agenda}},
        error => console.log(error)
    );
  }

  getViewerByToken(token: string) {
    this.publicAgendaService.getViewerByToken(this.agendaId, token).subscribe(
      (data: any) => {
        this.email = data.email;
        this.interestedSessionIds = data.sessions;
      },
      (error: any) => console.log(error)
    );
  }

  createToken() {
    this.publicAgendaService.createToken(this.agendaId, this.email).subscribe(
      (data: any) => this.router.navigate(['/public/agenda/' + this.agendaId + '/' + data.token]),
      (error: any) => console.log(error)
    );
  }
}
