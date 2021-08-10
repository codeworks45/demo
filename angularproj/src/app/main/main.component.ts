import { Component, OnInit, OnDestroy } from '@angular/core';
import { FlaskapiService } from '../flaskapi.service';
import { Subscription } from 'rxjs';
import { Post } from '../models/Post';
import { Input } from '@angular/core';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent implements OnInit,OnDestroy {
  // @Input() posts!: Post[]; //not b4
 //not b4
  constructor(private flaskApiService: FlaskapiService) { }
  // public posts: any[] = [];  b4
  // public posts: any[] = [];
  public posts: any[] = [];
  // public posts!: Array<Post>;
  public postsSubscription: Subscription = new Subscription;

  public getPosts(){
    this.postsSubscription = this.flaskApiService.getPosts().subscribe( p => {
      this.posts = (<any>p)["data"];
      // this.posts= p;
      // this.posts = p
      // this.posts = (<any>p)["data"];
      // this.posts = (<any>this.posts).data;
      // this.posts = (<any>p).data;
      // console.log(this.posts)
       console.log(this.posts);
      
    })
  }
  ngOnInit(): void {
    // this.posts.push(p)
  this.getPosts();
  }

  ngOnDestroy(): void{
    this.postsSubscription.unsubscribe();
  }

}
