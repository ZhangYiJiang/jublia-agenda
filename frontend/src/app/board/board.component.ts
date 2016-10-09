import { Input, Component, OnInit } from '@angular/core';

import {Session} from '../session/session';
import {Agenda} from '../agenda/agenda';

@Component({
  selector: 'board',
  templateUrl: './board.component.html',
  styleUrls: ['./board.component.css']
})
export class BoardComponent implements OnInit {
  @Input()
  agenda: Agenda;

	eventDates: Date[];
	eventTracks: string[];

  getEventDates(): Date[] {
  	let dates: Date[] = [];
  	let tempDate: Date = this.agenda.start;
  	while (tempDate <= this.agenda.end) {
  		dates.push(new Date(tempDate.getTime()));
  		tempDate.setDate(tempDate.getDate()+1);
  	}
  	return dates;
  }

  getEventTracks() : string[] {
  	if (!this.agenda.tracks || this.agenda.tracks.length === 0) {
  		return ['']; //return a track with no name as the default track
  	}else{
  		return this.agenda.tracks;
  	}
  }

  ngOnInit(): void {
  	this.eventDates = this.getEventDates();
  	this.eventTracks = this.getEventTracks();
  }
}
