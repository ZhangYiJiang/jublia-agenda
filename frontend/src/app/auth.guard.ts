import { Injectable } from '@angular/core';
import { Router, CanActivate } from '@angular/router';
import { DashBoardService } from './dash-board/dash-board.service.ts';

@Injectable()
export class LoggedInGuard implements CanActivate {
  constructor(private dashBoardService: DashBoardService) {}

  canActivate() {
    return this.dashBoardService.user.authed;
  }
}