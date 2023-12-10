export class AlreadyExists extends Error {
  constructor() {
    super("User with same login already exists");
    this.name = "AlreadyExists";
  }
}

export class RequestFailed extends Error {
  constructor(statusCode) {
    super(`Failed to executed request. Reason: ${statusCode}`);
    this.name = "RequestFailed";
  }
}

export class InvalidCredentials extends Error {
  constructor(credentials) {
    super("Invalid credentials");
    this.credentials = credentials;
  }
}


export class Unauthorized extends Error {
  constructor() {
    super("Unauthorized. Token not specified or invalid.");
  }
}


export class NotFound extends Error {
  constructor() {
    super("Requested entity not found");
  }
}
