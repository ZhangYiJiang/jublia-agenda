import { Component, Input, OnInit } from '@angular/core';

import { Session } from '../session/session';

@Component({
  selector: 'absolute-column',
  templateUrl: './absolute-column.component.html',
  styleUrls: ['./absolute-column.component.css']
})
export class AbsoluteColumnComponent implements OnInit {
	@Input() sessions: Session[];
	@Input() day: Date;
	@Input() track: string;

	displayedSessions: Session[];

	getDisplayedSessions(): Session[] {
		let displayed:Session[] = [];
		for (let session of this.sessions) {
			if (session.pending === false 
				//add session to every track if it doesn't have a specific track
				&& (!session.track || session.track === this.track || session.track === '') 
				&& (session.start.toDateString() === this.day.toDateString() || session.end.toDateString() === this.day.toDateString()))
				displayed.push(session);
		}
		return displayed;
	}

	ngOnInit(): void {
  	this.displayedSessions = this.getDisplayedSessions();
  }
}
