import { Input, Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';

import { Session } from '../session/session';
import { Agenda } from '../agenda/agenda';
import { AgendaService } from '../agenda/agenda.service';

import * as _ from 'lodash';

@Component({
  selector: 'analytics',
  templateUrl: './analytics.component.html',
  styleUrls: ['./analytics.component.css']
})
export class AnalyticsComponent implements OnInit{
  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private agendaService: AgendaService) { }
  
  agenda: Agenda;
  analyticsData: any;
  analyticsDataCombinedY: any[] = [];
  analyticsDataCombinedX: any[] = [];
  agendaId: number;
  
  ngOnInit() {
    this.route.params.forEach((params: Params) => {
      // (+) converts string 'id' to a number
      let id = +params['id'];
      this.agendaId = id;
      this.getAgendaData(id);
    });
  }

  getAgendaData(id: number) {
    this.agendaService.getAgendaById(id).subscribe(
        agenda => {if (agenda.published) {this.agenda = agenda}},
        error =>  console.log(error)
    );

    this.agendaService.getAgendaAnalytics(id).subscribe(
        data => this.processRawData(data),
        error =>  console.log(error)
    );
  }

  processRawData(rawData: {}) {
    this.analyticsData = rawData;

    let combinedObj = {};

    _.forOwn(rawData, function(value: {}, key: string) {
      combinedObj = _.mergeWith(combinedObj, value, (objValue: number, srcValue: number) => {
        if(objValue == null || srcValue == null || _.isNaN(objValue)) {
          return 0;
        } else {
          return objValue + srcValue;
        }
      });
    });

    this.analyticsDataCombinedY = _.values(combinedObj);
    this.analyticsDataCombinedX = _.keys(combinedObj);
  }
}
