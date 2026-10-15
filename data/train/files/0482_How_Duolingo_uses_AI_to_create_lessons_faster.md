# How Duolingo uses AI to create lessons faster

Источник: https://blog.duolingo.com/large-language-model-duolingo-lessons/

You’ve probably heard plenty of buzz on the internet about artificial intelligence, or AI, and how it's rapidly weaving its way into the tech products you use daily. Here at Duolingo, we've been using AI for years, and we’ve recently brought the power of AI to our learners through Duolingo Max—but we’re also using AI behind the scenes to build courses faster and better than ever.
The type of AI we use is called a Large Language Model (LLM), and it’s very good at predicting the most likely way to complete a string of text, like a sentence. This is what’s at work on your phone when it suggests next words to type in text messages!
A Large Language Model “thinks” kind of like this:
| Partial sentence | Possible next word | Likelihood | 
|---|---|---|
| I really like French... | fries | very high | 
|  | movies | high | 
|  | movie | low | 
|  | the | very low | 
|  | are | almost impossible | 
With a powerful Large Language Model in the hands of Duolingo’s teaching experts, we can generate vast amounts of content for our lessons with the click of a button.
How AI helps us create lessons
AI is nothing new at Duolingo. In fact, we’ve been using an AI model called "Birdbrain" to make sure the exercises you see on Duolingo are at the perfect difficulty level based on your strengths and weaknesses. Until now, every single exercise chosen by Birdbrain was written, reviewed, edited, and translated by human experts who constantly think about maximizing both the entertainment and learning value of every Duolingo lesson.
Today, we’ve moved into using AI to create these exercises. The Large Language Model can learn a lot from seeing the examples of Duolingo content we learning experts have already created, but it still needs a lot of help from us humans—in fact, we’re constantly adjusting the instructions we give the model. Think of AI as a wind up toy. If you wind it up, it’s sure to move, but if we want it to go in the right direction, we’ve got to build some guardrails.
Here’s how our AI system works: We write a “prompt,” or a set of detailed commands, that “explains” to the AI model how to write a given Duolingo exercise. You can think of the prompt as kind of like a Mad Lib for generating Duolingo lessons.
Write an exercise that uses the word VISITAR in SPANISH.
    
Rules:
    
1. The exercise must have two answer options.
    
2. The exercise must be fewer than 75 characters.
    
3. The exercise must be written in A2 CEFR level SPANISH.
    
4. The exercise must contain THE PRETERITE TENSE and THE IMPERFECT TENSE.
    
Go!
Some of the instructions are the same for a particular exercise type. For example, Rules 1 and 2 don't change. Other instructions change for every new exercise we generate: Rule 3 changes depending on the course we’re working on and the difficulty level we’re generating for. Rule 4 depends on the exact focus of the lesson. After we put all the fixed and the variable information together into one prompt, the model will produce an exercise with one click.
By developing these prompts and editing the output, AI is a powerful tool at our disposal. Like any innovative tool, with a good operator, it can bring our in-house teachers convenience, speed, and productivity:
- Convenience: We used to carry maps and atlases in our cars to use on long road trips. Then, we carried bulky plug-in GPSes that sat on our dashboards. Now, we have map apps on our smartphones.
- Speed: Calculators have made it so much faster to do simple arithmetic that would take much longer to do in our heads or on paper. Yet, there was panic when calculators were introduced into classrooms. How would students learn math if they had such a powerful tool!? It turned out, though, that students using a calculator still needed to understand the underlying mathematical processes to get the right answer. The tool was only as powerful as the user’s understanding of it.
- Productivity: Some workplace tools can spur productivity with several different applications. For example, spreadsheets have been available for a long time, starting on paper solely for accounting purposes. But, when they moved to a digital format, they began to fill in the gaps in many more cases. In my work at Duolingo, I use spreadsheets to organize feedback from colleagues, track vocabulary in the courses I work on, and a few years ago, I even used them to write the content on the app!
All these innovations changed the way we work and interact with challenges, but ultimately, they made our work more convenient, faster, and more productive.
What does AI look like in action?
Step 1: Curriculum design
The Learning Designer plans out the theme, grammar, vocabulary, and exercise types for a given lesson. For example, they may want to create a Spanish lesson with the theme “nostalgic memories” because it fits well with the grammar focus of the preterite and imperfect.
Step 2: Prepping the AI tool
It’s time to fill in the blanks of our Mad Lib. Thanks to our amazing engineers, some blanks get filled in automatically (like the language, CEFR level, and theme of nostalgic memories). The Learning Designer fills in a few more blanks, such as the exercise type and the grammar focus, to steer the AI in the right direction.
Step 3: Generation and tweaks
In a matter of seconds, the AI model outputs ten exercises that fit the difficulty level, the grammar, and the theme.
    1) Ayer visité la playa de mi infancia. Cuando era niño, visitaba esa playa a menudo.
2) La semana pasada, fuimos al cine el sábado. Antes, íbamos al cine los viernes.
3) Solía leer muchos libros de aventuras. El mes pasado, leí un libro de aventuras emocionante.
4) Ayer, cocinó paella para la cena. Mi papá cocinaba paella los domingos.
5) La escuché de nuevo esta mañana. Escuchaba esa canción todos los días.
6) Anoche, vi una película de terror clásica. Veía películas de terror en mi juventud.
7) Montamos en bicicleta el fin de semana pasado. Mis amigos y yo montábamos en bicicleta juntos.
8) Mi familia y yo siempre veraneábamos en la playa. El verano pasado, veraneamos en la montaña.
9) Encontré una moneda antigua en un cajón la semana pasada. De pequeño, coleccionaba monedas.
10) Aprendía a tejer con mi abuelita cada invierno. Ayer, tejí una bufanda para ella.
The Learning Designer then chooses their three favorite sentences, but they can still make edits before they go into the app. If you know some Spanish, you probably notice that all these exercises follow the rules, but some of them sound a little stilted or unnatural. In this case, the Learning Designer would probably make some tweaks for naturalness, learning value, and appropriate vocabulary. Ultimately, our Spanish teaching experts always have the final say.
The benefits of using AI for lesson creation
At the time of writing this, Duolingo has fewer than 1,000 employees and over 21 million daily users. That means we need to prioritize ruthlessly with the resources we have to develop the best education in the world and make it universally available!
Currently, building, updating, and maintaining Duolingo courses takes a considerable amount of time, with most courses releasing new content only a few times a year. If we can produce quality content faster, we can
- Delve deeper into the CEFR scale to teach more advanced concepts
- Allocate resources to more features like Stories, DuoRadio, and a host of ideas still in the works
- Expand our focus to smaller courses that aren’t often in the spotlight but which still have a dedicated band of Duolingo learners
We're always striving to improve our content creation speed, and giving our human teaching experts a tool like a Large Language Model helps us bring you more of the Duolingo you love, faster and better than ever!
