import { Input, Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';

import { Session } from '../session/session';
import { Agenda } from './agenda';
import { AgendaService } from '../agenda/agenda.service';

@Component({
  selector: 'agenda',
  templateUrl: './agenda.component.html',
  styleUrls: ['./agenda.component.css']
})
export class AgendaComponent implements OnInit{
  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private agendaService: AgendaService) { }
  
  agenda: Agenda;
  
  ngOnInit() {
    console.log('onInit');
    console.log(this.agenda);
    this.route.params.forEach((params: Params) => {
      let id = params['id'];
      this.agenda = this.agendaService.getAgendaById(id);
     /* this.agendaService.getAgendaById(id).then(agenda => {
        this.agenda = agenda;
        console.log('added agenda');
        console.log(this.agenda);
      });*/
    });
  }
}
