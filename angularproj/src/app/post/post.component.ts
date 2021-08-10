import { Component, OnInit, OnDestroy } from '@angular/core';
import { FlaskapiService } from "../flaskapi.service";
import { ActivatedRoute, Router } from "@angular/router";
import { Subscription } from 'rxjs';
import { Post } from "../models/Post";
import { FormGroup, FormControl, Validators } from "@angular/forms";

@Component({
  selector: 'app-post',
  templateUrl: './post.component.html',
  styleUrls: ['./post.component.css']
})
export class PostComponent implements OnInit {
 //picked from here
//  post : Post ={
//    id: '',
//    title: '',
//    content: '',
//    cover: '',
//    covername: ''
//  }
 constructor(private flaskApiService: FlaskapiService, private route: ActivatedRoute, private router: Router) { 
    
}

  public currentId: any = this.route.snapshot.paramMap.get("id");
  public postSubscription: Subscription = new Subscription;
  public editSubscription: Subscription = new Subscription;
  public post!: Post;
  public editMode: boolean = false;
  public image: any;
  public busy!: boolean;

  public editForm = new FormGroup({
    id: new FormControl('', Validators.required),
    title: new FormControl('', Validators.required),
    content: new FormControl('',  Validators.required),
    oldcover: new FormControl('',  Validators.required),  
    covername: new FormControl('', Validators.required)
  });

  public handleInput($event: Event){
    //getting the image or files
    const target= $event.target as HTMLInputElement;
    const file: File = (target.files as FileList)[0];
    this.image = file;
    // this.image = $event.target["files"];
    console.log(this.image);
  }


  public enableEdit(){
    this.editMode = !this.editMode;
  }


  public editPost(formData: Post){
    this.busy = true;
    this.editSubscription = this.flaskApiService.editPost(formData, this.image).subscribe((res: any) => {
      this.busy = false;
      console.log(res)
    })
  }


  public getPostById(){
    this.postSubscription = this.flaskApiService.getPost(this.currentId).subscribe( res => {
      this.post = (<any>res)["data"];
      console.log(this.post + "OKAYYY")
      // this.post = (<any>res)["data"]; //check res["data"];
      console.log("Hello" + this.post)
      this.editForm.setValue({
        title: this.post.title,
        content: this.post.content,
        id: this.post.id,
        oldcover: this.post.cover,
        covername: this.post.covername
      })
    })
  }


  public deletePost(postId: any){
    this.flaskApiService.deletePost(postId).subscribe((res: any) => {
      console.log(res);
      this.router.navigate(["/"]);
    })
  }



  ngOnInit(): void {
    // this.getPostById();
  }
  ngOnDestroy(): void {
    this.postSubscription.unsubscribe();
  }

}
// setTimeout(() => { this.editForm.setValue({
//   title: this.post.title,
//   content: this.post.content,
//   id: this.post.id,
//   oldcover: this.post.cover,
//   covername: this.post.covername
// })
// } , 2000 );}
// )