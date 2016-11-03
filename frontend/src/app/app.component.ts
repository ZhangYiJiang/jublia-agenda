import { Component, ViewContainerRef, ViewEncapsulation } from '@angular/core';
import { Router, ActivatedRoute, NavigationStart,Event } from '@angular/router';

import { DashBoardService } from './dash-board/dash-board.service';
import { Location } from '@angular/common';

import { GlobalVariable } from './globals';

import { Overlay } from 'angular2-modal';
import { Modal } from 'angular2-modal/plugins/vex';


import '../../public/css/vex.css';
import '../../public/css/vex-theme-default.css';
import '../../public/css/styles.css';

@Component({
  selector: 'my-app',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  appName: string = GlobalVariable.APP_NAME;
  user = this.dashBoardService.currentUser;
  isOnDashBoard = true;
  isPublic = false;

  constructor ( 
    private router: Router,
    private route: ActivatedRoute,
  	private dashBoardService: DashBoardService,
    overlay: Overlay, 
    vcRef: ViewContainerRef, 
    public modal: Modal) {
    overlay.defaultViewContainer = vcRef;
    router.events.subscribe(event => {
      if (event instanceof NavigationStart) {
        if (event.url === '/'){
          this.isOnDashBoard = true;
          this.isPublic = false;
        }else if (event.url.substring(0, 15) === '/public/agenda/'){
          this.isPublic = true;
          this.isOnDashBoard = false;
        } else {
          this.isOnDashBoard = false;
          this.isPublic = false;
        }
      }
    })
  }

  logOut() {
  	console.log('log out');
    this.dashBoardService.logOut();
    this.router.navigate(['']);
  }
}
