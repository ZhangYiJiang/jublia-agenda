import { Component } from '@angular/core';
import '../../public/css/styles.css';
import { DashBoardService } from './dash-board/dash-board.service';

import { GlobalVariable } from './globals';

@Component({
  selector: 'my-app',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  appName: string = GlobalVariable.APP_NAME;
  user = this.dashBoardService.user;

  constructor (private dashBoardService: DashBoardService) {}

  logOut() {
  	console.log('log out');
    this.dashBoardService.logOut();
  }
}
