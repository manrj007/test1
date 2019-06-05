import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { URL, PORT } from '../constants/app.constants';
@Injectable({
  providedIn: 'root'
})
export class ArgusService {
  emitResult = new BehaviorSubject<any>([]);
  emitSelectedSenteces = new BehaviorSubject<string>('');
  url = URL;
  port = PORT;
  constructor(private http: HttpClient) { }

  saveToLocal(fileName, fileData) {
    const httpOptions = {
      headers: new HttpHeaders({
          'Content-Type': 'multipart/form-data',
      })
    };
    const formData: FormData = new FormData();
    formData.append('file', fileData, fileName);

    this.http.post(`${this.url}:${this.port}/upload`, formData,  httpOptions).subscribe((data) => {
      console.log(data);
    });
  }
}
