if (!Array.prototype.find) {
    Object.defineProperty(Array.prototype, "find", {
        value: function(callback) {
          for (var i = 0; i < this.length; i++) {
            if (callback.call(arguments[1], this[i], i, this)) {
              return this[i];
            }
          }
          return undefined;
        }
    });
}
