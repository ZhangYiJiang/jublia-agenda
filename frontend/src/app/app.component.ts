import { Component, ViewContainerRef, ViewEncapsulation } from '@angular/core';
import { Router } from '@angular/router';
import { Location } from '@angular/common';

import { DashBoardService } from './dash-board/dash-board.service';

import { GlobalVariable } from './globals';

import { Overlay } from 'angular2-modal';
import { Modal } from 'angular2-modal/plugins/vex';

import '../../public/css/styles.css';

@Component({
  selector: 'my-app',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  appName: string = GlobalVariable.APP_NAME;
  user = this.dashBoardService.currentUser;

  constructor ( 
    private router: Router,
  	private dashBoardService: DashBoardService,
    private location: Location,
    overlay: Overlay, 
    vcRef: ViewContainerRef, 
    public modal: Modal) {
    overlay.defaultViewContainer = vcRef;
    this.router.events.pairwise().subscribe((e) => {
            console.log(e);
        });
  }

  logOut() {
  	console.log('log out');
    this.dashBoardService.logOut();
    this.router.navigate(['']);
  }

  goBack() {
    this.user.agenda = false;
    //this.location.back();
    this.location.go('/');
  }
}
