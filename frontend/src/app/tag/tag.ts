export class Tag {
  id: number;
  name: string;
  url: string;
  // only on front-end
  toggle: boolean;
  // if tag is used by any session
  used: boolean;
}