import { Injectable } from '@angular/core';
import {ContainerData} from "../absolute-column/absolute-column.component";

@Injectable()
export class DOMUtilService {
  hasClass(element: Element, cls: string): boolean {
    return element.classList.contains(cls);
  }

  getSessionIdFromDOM(el: HTMLElement): number {
    return parseInt(el.dataset['sessionId']);
  }
  
  getContainerData(el: HTMLElement): ContainerData {
    return JSON.parse(el.dataset['container']);
  }
}