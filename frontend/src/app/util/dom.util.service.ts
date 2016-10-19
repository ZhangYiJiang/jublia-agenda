import { Injectable } from '@angular/core';

@Injectable()
export class DOMUtilService {
  hasClass(element: Element, cls: string): boolean {
    return (' ' + element.className + ' ').indexOf(' ' + cls + ' ') > -1;
  }

  getSessionIdFromDOM(el: HTMLElement): number {
    return parseInt(el.getAttribute('data-session-id'))
  }

  getContainerStartAt(el: HTMLElement): number {
    return parseInt(el.getAttribute('data-container-start-at'));
  }

  getContainerGlobalStartAt(el: HTMLElement): number {
    return parseInt(el.getAttribute('data-container-global-start-at'));
  }

  getContainerTrack(el: HTMLElement): number {
    return +el.getAttribute('data-track-id');
  }

  getContainerDate(el: HTMLElement): Date {
    return new Date(el.getAttribute('data-date'));
  }
}