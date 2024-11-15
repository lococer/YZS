<template>
  <div>
    <div>{{ movieId }}</div>
    <div class="comment-component">
      <h3>评论列表</h3>
      <a-list>
        <a-list-item>
          <a-comment
            v-for="(comment, index) in comments"
            :key="index"
            :author="comment.username"
            :avatar="comment.avatar"
          >
            <template #content>
              <p>{{ comment.comment }}</p>
            </template>
          </a-comment>
        </a-list-item>
      </a-list>

      <h4>发表评论</h4>
      {{ currentUsername }}
      <a-form @submit.prevent="submitComment">
        <a-textarea
          v-model:value="newComment.content"
          placeholder="写下你的评论..."
        />
        <a-button type="primary" html-type="submit">提交</a-button>
      </a-form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { Comment, List, Avatar, Form, Button, Input } from 'ant-design-vue';

export default {
    name: 'myComments',
    data() {
        return {
            comments: [
                // 初始评论列表
                { username: '用户A', comment: '这是一条评论' },
                { username: '用户B', comment: '这是另一条评论' },
                // ...更多评论
            ],
            newComment: {
                author: '匿名用户', // 可以根据实际情况获取用户信息
                content: ''
            },
            // movieId: 123,
        };
    },
    components: {
        'a-comment': Comment,
        'a-list': List,
        'a-list-item': List.Item,
        'a-form': Form,
        'a-textarea': Input.TextArea,
        'a-button': Button,
    },
    methods: {
        submitComment() {
            // alert(`${this.currentUsername}`);
            if (this.newComment.content.trim() === '') {
                alert('评论内容不能为空');
                return;
            }
            try{
                console.log(this.movieId, this.currentUsername, this.newComment.content);
                axios.post(`http://127.0.0.1:5001/api/movies/addcomment`, {
                    movieid: this.movieId,
                    username: this.currentUsername,
                    comment: this.newComment.content
                })
               .then(response => {
                    // this.comments.push(response.data);
                    // this.newComment.content = '';
                    this.fetchComments();
                })
               .catch(error => {
                    console.log(error);
                });
            }catch(e){
                alert('评论失败');
                console.log(e);
            }
        },
        fetchComments() {
            // 调用接口获取评论列表
            console.log(this.movieId);
            axios.get(`http://127.0.0.1:5001/api/movies/comments/${this.movieId}`)
               .then(response => {
                    this.comments = response.data;
                })
               .catch(error => {
                    console.log(error);
                });
        }
    },
    props:{
        movieId: {
            type: Number,
            required: true,
        },
        currentUsername:{
            type: String,
            required: true,
        }
    },
    watch:{
        movieId:{
            immeditate: true,
            handler(newval){
                if(newval){
                    this.fetchComments();
                }
            }
        }
    }
};
</script>

<style scoped>
.comment-component {
  margin: 20px;
  padding: 20px;
  border: 1px solid #e8e8e8;
  border-radius: 4px;
  background-color: #fff;
}

.comment-list {
  margin-top: 20px;
}

.comment-item {
  margin-bottom: 10px;
  padding: 10px;
  border-bottom: 1px solid #e8e8e8;
}

.comment-author {
  font-weight: bold;
  margin-bottom: 5px;
}

.comment-content {
  color: #333;
}

.comment-input {
  width: 100%;
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  resize: vertical;
}

.comment-submit {
  display: block;
  width: 100%;
  padding: 10px;
  background-color: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.comment-submit:hover {
  background-color: #40a9ff;
}
</style>