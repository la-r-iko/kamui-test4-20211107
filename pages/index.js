   // pages/index.js
   import React from 'react';
   import { useRouter } from 'next/router';

   export default function Home() {
     const router = useRouter();

     const navigateToCustomPage = () => {
       router.push('/custom');
     };

     const navigateToSchedule = () => {
       router.push('/lessons/schedule');
     };

     return (
       <div>
         <h1>Welcome to the Home Page!</h1>
         <button onClick={navigateToCustomPage}>Go to Custom Page</button>
         <button onClick={navigateToSchedule}>Go to Schedule</button>
       </div>
     );
   }