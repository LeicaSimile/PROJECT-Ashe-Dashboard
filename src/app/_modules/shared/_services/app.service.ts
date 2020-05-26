import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AppService {
  public externalUrl = 'externalRedirect';
  public baseApiUrl = 'http://localhost:3000/api/';
  CLIENT_ID = '';
  user: any = false;

  constructor() { }
}
