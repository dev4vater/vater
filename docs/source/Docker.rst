
Getting Started with Docker
===========================

Docker is an open platform for developing, shipping, and running applications. 
Docker enables you to separate your applications from your infrastructure so you can deliver software quickly.
With Docker, you can manage your infrastructure in the same ways you manage your applications.

Containers
==========

Docker provides the ability to package and run an application in a loosely isolated environment called a **container**. 
The isolation and security allows you to run many containers simultaneously on a given host.
Docker provides tooling and a platform to manage the lifecycle of your containers:

- Develop your application and its supporting components using containers.
- The container becomes the unit for distributing and testing your application.
- When you’re ready, deploy your application into your production environment, as a container or an orchestrated service.

Images
~~~~~~

An image is a read-only template with instructions for creating a Docker container. Often, an image is based on another image, with some additional customization. 
To build your own image, you create a Dockerfile with a simple syntax for defining the steps needed to create the image and run it.
Each instruction in a Dockerfile creates a layer in the image. When you change the Dockerfile and rebuild the image, only those layers which have changed are rebuilt.

Containers and Images
~~~~~~~~~~~~~~~~~~~~~~
A container is a runnable instance of an image. You can create, start, stop, move, or delete a container using the Docker API or CLI. 
A container is defined by its image as well as any configuration options you provide to it when you create or start it.

Practical Applications
======================

- A developer writes code locally and shares their work using Docker containers.
- A developer uses Docker to push their applications into a test environment and execute automated and manual tests.
- When developers find bugs, they can fix them in the development environment and redeploy them to the test environment for testing and validation.
- When testing is complete, the develoepr can simply push the updated image to the production environment.

More Information: 

- `Docker <https://docs.docker.com/get-started/overview/>`__
