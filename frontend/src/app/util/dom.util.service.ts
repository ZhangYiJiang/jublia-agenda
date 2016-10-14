import { Injectable } from '@angular/core';

@Injectable()
export class DOMUtilService {
  hasClass(element: Element, cls: string): boolean {
    return (' ' + element.className + ' ').indexOf(' ' + cls + ' ') > -1;
  }
}