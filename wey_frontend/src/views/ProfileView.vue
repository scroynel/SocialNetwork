<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-1">
            <div class="p-4 bg-white border border-gray-200 text-center rounded-lg content-center">
                <img :src="user.get_avatar" class="mb-6 rounded-full mx-auto">

                <p class="text-center"><strong>{{ user.name }}</strong></p>

                <div class="mt-6 flex space-x-8 justify-around">
                    <RouterLink :to="{name: 'friends', params: {id: user.id}}" class="text-xs text-gray-500">{{ user.friends_count }} friends</RouterLink>
                    <p class="text-xs text-gray-500">{{ user.posts_count }} posts</p>
                </div>

                <div class="mt-6">
                    <button class="inline-block py-4 px-6 bg-purple-600 text-xs text-white rounded-lg" v-if="userStore.user.id !== user.id && can_send_friendship_request" @click="sendFriendshipRequest">Send friendship request</button>
                    <button class="inline-block mt-4 py-4 px-6 bg-purple-600 text-xs text-white rounded-lg" v-if="userStore.user.id !== user.id" @click="sendDirectRequest">Send direct request</button>
                    <RouterLink to="/profile/edit" class="inline-block mr-2 py-4 px-6 bg-purple-600 text-xs text-white rounded-lg" v-if="userStore.user.id === user.id">Edit profile</RouterLink>
                    <button class="inline-block py-4 px-6 bg-red-600 text-xs text-white rounded-lg" v-if="userStore.user.id === user.id" @click="logout">Log out</button>
                </div>
            </div>
        </div>
        
        <div class="main-center col-span-2 space-y-4">
            <div v-if="userStore.user.id === user.id" class="bg-white border border-gray-200 rounded-lg">
                <form v-on:submit.prevent="submitForm" method="POST">
                    <div class="p-4">
                        <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="What are you thinking about?"></textarea>

                        <div id="preview" v-if="url">
                            <img :src="url" class="w-[100px] mt-3 rounded-xl"/>
                        </div>
                    </div>

                    <div class="p-4 border-t border-gray-100 flex justify-between">
                        <label class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">
                            <input type="file" ref="file" @change="onFileChange">
                            Attach image
                        </label>
                        <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Post</button>
                    </div>
                </form>
                
            </div>

            <div v-for="post in posts" v-bind:key="post.id" class="p-4 bg-white border border-gray-200 rounded-lg">
                <FeedItem v-bind:post="post"/>
            </div> 
        </div>

        <div class="main-right col-span-1 space-y-4">
            
            <PeopleYouMayKnow />

            <Trends />

        </div>
    </div>
</template>

<style scoped>
    input[type="file"] {
        display: none;
    }
</style>

<script>
import axios from 'axios'
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import Trends from '../components/Trends.vue'
import FeedItem from '../components/FeedItem.vue'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toasts'
import { RouterLink } from 'vue-router'

export default {
    name: 'ProfileView',
    setup() {
        const userStore = useUserStore()
        const toastStore = useToastStore()

        return {
            userStore,
            toastStore,
            
        }
    },
    components: {
        PeopleYouMayKnow,
        Trends,
        RouterLink,
        FeedItem
},
    data() {
        return {
            posts: [],
            user: {},
            can_send_friendship_request: null,
            body: '',
            url: null,
        }
    },
    mounted() {
        this.getFeed()
        console.log('mounted')
    },
    
    updated() {
        console.log('updated')
    },  
    // for nav in App.vue that avatar of user on click refresh page with correct id
    watch: {
        '$route.params.id': {
            handler: function() {
                console.log('sgdfjkgdf')

                this.getFeed()
            },
            deep: true,
            immediate: true
        }
    },
    methods: {
        onFileChange(e) {
            const file = e.target.files[0];
            this.url = URL.createObjectURL(file);
        },
        sendDirectRequest() {
            console.log('sendDirectRequest')

            axios
                .get(`/api/chat/${this.$route.params.id}/get-or-create/`)
                .then(response => {
                    console.log(response.data)

                    this.$router.push('/chat')
                })
                .catch(error => {
                    console.log('error', error)
                })

        },

        sendFriendshipRequest() {
            axios
                .post(`/api/friends/${this.$route.params.id}/request/`)
                .then(response => {
                    console.log('data', response.data)

                    this.can_send_friendship_request = False

                    if (response.data.message == 'request already sent') {
                        this.toastStore.showToast(5000, 'The request has already been sent!', 'bg-emerald-300-')
                    } else {
                        this.toastStore.showToast(5000, 'The request was sent', 'bg-emerald-300-')
                    }
                })
                .catch(error => {
                    console.log('error', error)
                })
        },
        getFeed() {
            axios
                .get(`/api/posts/profile/${this.$route.params.id}/`)
                .then(response => {
                    console.log('data', response.data)

                    this.posts = response.data.posts
                    this.user = response.data.user
                    this.can_send_friendship_request = response.data.can_send_friendship_request

                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        submitForm() {
            console.log('submitForm', this.body)

            let formData = new FormData()
            formData.append('image', this.$refs.file.files[0])
            formData.append('body', this.body)

            axios
                .post('/api/posts/create/', formData, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    }
                })
                .then(response => {
                    console.log('data', response.data)

                    this.posts.unshift(response.data)

                    this.user.posts_count += 1
                    this.body = ''
                    this.url = null
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        logout() {
            console.log('logout')

            this.userStore.removeToken()

            this.$router.push('/login')
        }
    }
}
</script>

