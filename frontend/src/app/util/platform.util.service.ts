import { Injectable } from '@angular/core';
import {BrowserModule} from "@angular/platform-browser";

@Injectable()
export class PlatformUtilService {
  constructor(
    browser: BrowserModule,
  ){}
  
  platformShortcut(key: string = null): string {
    if (window.navigator.userAgent.toLowerCase().includes('macintosh')) {
      return key ? '⌘-' + key : '⌘';
    } else {
      return key ? 'Ctrl+' + key : 'Ctrl';
    }
  }
  
  copyShortcut(): string {
    return this.platformShortcut('C');
  }
}