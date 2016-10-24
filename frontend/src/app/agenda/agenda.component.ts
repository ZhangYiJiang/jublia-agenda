import { Input, Component, OnInit, ViewContainerRef, ViewEncapsulation, ViewChild, TemplateRef } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';

import { Session } from '../session/session';
import { Agenda } from './agenda';
import { AgendaService } from '../agenda/agenda.service';

import { overlayConfigFactory } from 'angular2-modal';
import { Overlay } from 'angular2-modal';

import {
  VEXBuiltInThemes,
  Modal,
  DialogPreset,
  DialogFormModal,
  DialogPresetBuilder,
  VEXModalContext,
  VexModalModule,
  providers
} from 'angular2-modal/plugins/vex';

@Component({
  selector: 'agenda',
  templateUrl: './agenda.component.html',
  styleUrls: [
    './agenda.component.css',
    '../session/css/vex.css',
    '../session/css/vex-theme-default.css'
  ]
})
export class AgendaComponent implements OnInit{
  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private agendaService: AgendaService,
    public modal: Modal) { }
  
  agenda: Agenda;

  @ViewChild('templateRef') public templateRef: TemplateRef<any>;
  
  ngOnInit() {
    this.route.params.forEach((params: Params) => {
      let id = params['id'];
      this.getAgendaById(id);
    });
  }

  updateAgenda(event: any) {
    console.log(event);
    if(typeof event.name === 'string') {
      this.agendaService.updateAgenda(this.agenda.id, {name: event.name})
        .subscribe(
          agenda => this.agenda = agenda,
          error => console.log(error)
        );
    }
  }

  showAgendaSettings(event: DocumentEvent) {
    this.modal
      .open(this.templateRef, overlayConfigFactory({ isBlocking: false }, VEXModalContext));
  }

  getAgendaById(id: number) {
    this.agendaService.getAgendaById(id).subscribe(
        agenda => this.agenda = agenda,
        error =>  console.log(error)
    );
  }

  publishAgenda() {
    this.agendaService.publishAgenda(this.agenda.id).subscribe(
      agenda => this.agenda = agenda,
      error =>  console.log(error)
    );
  }

  unpublishAgenda() {
    this.agendaService.unpublishAgenda(this.agenda.id).subscribe(
      agenda => this.agenda = agenda,
      error =>  console.log(error)
    );
  }
}
